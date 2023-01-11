import smartpy as sp


class testChecksignature(sp.Contract):
    def __init__(self, **kargs):

        # thingToSign = sp.pack(sp.record(o='Hello World', n='hello', c=0))
        # msg = sp.concat([sp.utils.bytes_of_string('Hello World'), sp.utils.bytes_of_string(
        #     'hello'), sp.utils.bytes_of_string(string_of_nat(0))])
        # self.init(currentValue='Hello World', counter=0, bossPublicKey=boss_pk,
        #           thingToSign=thingToSign, msg=msg, hello=hello, hello_world=hello_world, count=count)

        # self.init(metadata=metadata, currentValue='Hello World',
        #           counter=0, bossPublicKey=boss_pk)

        self.init(**kargs, currentValue='Hello World', counter=0)

        # Build the TZIP-016 contract metadata
        # This is helpful to get the off-chain views code in json format
        contract_metadata = {
            "name": "Extended FA2 template contract",
            "description" : "This contract tries to simplify and extend the "
                "FA2 contract template example in smartpy.io v0.9.1",
            "version": "v1.0.0",
            "authors": ["J"],
            "interfaces": ["TZIP-012", "TZIP-016"],
            "views": [
                self.get_msg_bytes,
                self.get_pk,
                self.get_value,
                self.get_counter]
        }
        self.init_metadata("contract_metadata", contract_metadata)

    @sp.entry_point
    def setCurrentValue(self, params):
        # We will also need Michelson SELF and CHAIN_ID to avoid all replay attacks:
        thingToSign = sp.pack(
            sp.record(o=self.data.currentValue, n=params.newValue, c=self.data.counter))

        sp.verify(sp.check_signature(self.data.bossPublicKey,
                  params.userSignature, thingToSign))
        self.data.currentValue = params.newValue
        self.data.counter = self.data.counter + 1

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
    c1 = testChecksignature(bossPublicKey=rightful_owner.public_key, metadata=sp.utils.metadata_of_url(
        "ipfs://Qme9L4y6ZvPwQtaisNGTUE7VjU7PRtnJFs8NjNyztE3dGT"))

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
    # , metadata=sp.utils.metadata_of_url("ipfs://Qme9L4y6ZvPwQtaisNGTUE7VjU7PRtnJFs8NjNyztE3dGT")))
