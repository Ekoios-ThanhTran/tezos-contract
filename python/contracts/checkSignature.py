import smartpy as sp

# def string_to_raw_bytes(x):
#     x_packed = sp.pack(x)
#     length = sp.len(x)
#     return sp.slice(x_packed, 6, sp.to_int(length) - 1)

# def int_to_raw_bytes(x):
#     x_packed = sp.pack(x)
#     length = sp.len(x)
#     return sp.slice(x_packed, 2, length - 1)

def string_of_nat(params):
    c   = sp.map({x : str(x) for x in range(0, 10)})
    x   = sp.local('x', params)
    res = sp.local('res', [])
    sp.if x.value == 0:
        res.value.push('0')
    sp.while 0 < x.value:
        res.value.push(c[x.value % 10])
        x.value //= 10
    return sp.concat(res.value)


class testChecksignature(sp.Contract):
    def __init__(self, **kargs):

        # thingToSign = sp.pack(sp.record(o='Hello World', n='hello', c=0))
        # msg = sp.concat([sp.utils.bytes_of_string('Hello World'), sp.utils.bytes_of_string(
        #     'hello'), sp.utils.bytes_of_string(string_of_nat(0))])
        # self.init(currentValue='Hello World', counter=0, bossPublicKey=boss_pk,
        #           thingToSign=thingToSign, msg=msg, hello=hello, hello_world=hello_world, count=count)

        # self.init(metadata=metadata, currentValue='Hello World',
        #           counter=0, bossPublicKey=boss_pk)

        # msg = sp.concat([sp.slice(sp.pack("Hello World"), 6, sp.len(sp.pack("Hello World")) - sp.nat(1)), sp.slice(sp.pack(
        #     "hello"), 6, sp.len(sp.pack("hello")) - sp.nat(1)), sp.slice(sp.pack(0), 2, sp.len(sp.pack(0)) - sp.nat(1))])
        msg = sp.concat([sp.pack("Hello World"), sp.pack("hello"), sp.pack(sp.int(69))])

        self.init(**kargs, currentValue='Hello World',
                  counter=0, count_bytes=sp.pack(sp.record(c=0)), msg=msg)

        # # Build the TZIP-016 contract metadata
        # # This is helpful to get the off-chain views code in json format
        # contract_metadata = {
        #     "name": "Extended FA2 template contract",
        #     "description": "This contract tries to simplify and extend the "
        #     "FA2 contract template example in smartpy.io v0.9.1",
        #     "version": "v1.0.0",
        #     "authors": ["J"],
        #     "interfaces": ["TZIP-012", "TZIP-016"],
        #     "views": [
        #         self.get_msg_bytes,
        #         self.get_pk,
        #         self.get_value,
        #         self.get_counter]
        # }
        # self.init_metadata("contract_metadata", contract_metadata)

    @sp.entry_point
    def setCurrentValue(self, params):
        # We will also need Michelson SELF and CHAIN_ID to avoid all replay attacks:
        # thingToSign = sp.pack(
        #     sp.record(o=self.data.currentValue, n=params.newValue, c=self.data.counter))

        thingToSign = sp.concat([sp.pack(self.data.currentValue), sp.pack(
            params.newValue), sp.pack(string_of_nat(self.data.counter))])

        # thingToSign = sp.concat([sp.slice(sp.pack(self.data.currentValue), 6, sp.len(sp.pack(self.data.currentValue)) - 1), sp.slice(sp.pack(
        #     params.newValue), 6, sp.len(sp.pack(params.newValue)) - 1), sp.slice(sp.pack(self.data.counter), 2, sp.len(sp.pack(self.data.counter)) - 1)])

        sp.verify(sp.check_signature(self.data.bossPublicKey,
                  params.userSignature, thingToSign))
        self.data.currentValue = params.newValue
        self.data.counter = self.data.counter + 1

    @sp.entry_point
    def setCountBytes(self, params):
        sp.set_type(params, sp.TRecord(
            c=sp.TNat).layout(("c")))
        self.data.counter = params.c
        self.data.count_bytes = sp.pack(sp.record(c=params.c))

    @sp.utils.view(sp.TBytes)
    def get_msg_bytes_utils(self, params):
        sp.set_type(params, sp.TString)
        sp.result(
            sp.pack(sp.record(o=self.data.currentValue, n=params, c=self.data.counter)))

    @sp.onchain_view(pure=True)
    def get_msg_bytes(self, params):
        sp.set_type(params, sp.TString)
        sp.result(
            sp.pack(sp.record(o=self.data.currentValue, n=params, c=self.data.counter)))

    @sp.onchain_view(pure=True)
    def get_pk(self):
        sp.result(self.data.bossPublicKey)

    @sp.onchain_view(pure=True)
    def get_value(self):
        sp.result(self.data.currentValue)

    @sp.onchain_view(pure=True)
    def get_counter(self):
        sp.result(self.data.counter)

# Tests


@sp.add_test(name="CheckSignature")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Check Signature")
    rightful_owner = sp.test_account("Alice")
    attacker = sp.test_account("Robert")
    c1 = testChecksignature(bossPublicKey=rightful_owner.public_key)

    scenario += c1
    # Let's build a successful call:
    #
    scenario.h2("Successful Call")
    first_message_packed = sp.pack(
        sp.record(o="Hello World", n="should work", c=0))
    sig_from_alice = sp.make_signature(
        secret_key=rightful_owner.secret_key, message=first_message_packed, message_format="Raw")
    c1.setCurrentValue(newValue="should work",
                       userSignature=sig_from_alice).run(valid=True)
    #
    scenario.h2("Replay Attack")
    scenario.p(
        "Trying to reuse the same signature is blocked by the value of the counter.")
    c1.setCurrentValue(newValue="should work",
                       userSignature=sig_from_alice).run(valid=False)
    #
    #
    scenario.h2("Signature From Wrong Secret Key")
    scenario.p("Signing the right thing from a different secret-key.")
    #
    #
    # Gives:
    second_message_packed = sp.pack(
        sp.record(o="should work", n="Hello again World", c=1))
    sig_from_bob = sp.make_signature(
        secret_key=attacker.secret_key, message=second_message_packed, message_format="Raw")
    c1.setCurrentValue(newValue="Hello again World",
                       userSignature=sig_from_bob).run(valid=False)
    #
    scenario.h2("Second Successful Call")
    scenario.p(
        "Showing that the previous call failed <b>because</b> of the secret-key (signing same bytes).")
    sig_from_alice = sp.make_signature(
        secret_key=rightful_owner.secret_key, message=second_message_packed, message_format="Raw")
    c1.setCurrentValue(newValue="Hello again World",
                       userSignature=sig_from_alice).run(valid=True)


sp.add_compilation_target("testChecksignature", testChecksignature(
    bossPublicKey=sp.key("edpkuHHFnHeakQBfdf5NBQEeeYringQdX5ejsczc56eEmYVZEHcaGF")))
# , metadata=sp.utils.metadata_of_url("https://raw.githubusercontent.com/Ekoios-ThanhTran/tezos-contract/main/metadata/checkSignature.json")))
