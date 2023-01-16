// import { InMemorySigner } from '@taquito/signer';
// import { char2Bytes } from '@taquito/utils';

const { InMemorySigner } = require('@taquito/signer');
const { char2Bytes } = require('@taquito/utils');

// import { TezosToolkit } from '@taquito/taquito';
// import { Tzip16Module } from '@taquito/tzip16';
// import { tzip16 } from '@taquito/tzip16';

const { TezosToolkit } = require('@taquito/taquito');
const { Tzip16Module } = require('@taquito/tzip16');
const { tzip16 } = require('@taquito/tzip16');

async function offChainView(contractAddr) {
    const Tezos = new TezosToolkit('https://ghostnet.ecadinfra.com/');
    Tezos.addExtension(new Tzip16Module());

    const contract = await Tezos.contract.at(contractAddr, tzip16);

    const metadata = await contract.tzip16().getMetadata();

    console.log(metadata);

    const metadataViews = await contract.tzip16().metadataViews();
    // const viewResult = await metadataViews.get_msg_bytes().executeView([["hello"]]);
    // const viewResult = await metadataViews.get_pk().executeView();

    console.log(metadataViews)
    // console.log(viewResult)

}

function create_msg(arr) {
    return arr.reduce((pre, cur) => `${pre}0501${("00000000" + cur.length.toString(16)).slice(-8)}${char2Bytes(cur)}`, "")
}

async function signMsg() {
    const signer = await InMemorySigner.fromSecretKey("edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk");
    const newValue = "a".repeat(1000);
    const formattedInput = [
        '3sjdhfkhsdkfkasehfsdaksjdioejdsldjoiajsdiojsaoidjasjdjhasldljasdlj1231293877',
        newValue,
        '4'
    ];

    // The bytes to sign
    // const bytes = char2Bytes(formattedInput) + Number(69).toString(16);

    const bytes = create_msg(formattedInput);


    // console.log(bytes);

    // const bytes = STRING_OF_BYTES;
    const signature = await signer.sign(bytes);

    console.log(signature)
    return {
        signature,
        newValue,
    };
}

async function callContract() {
    const Tezos = new TezosToolkit('https://ghostnet.ecadinfra.com/');
    Tezos.setProvider({ signer: await InMemorySigner.fromSecretKey('edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk') });

    const res = await signMsg();
    

    const contract = await Tezos.contract.at('KT1EZjdjzH7foZgGFywHJtS7Dak7tF5gBVD6');
    const op = await contract.methods.setCurrentValue(res.newValue, res.signature.prefixSig).send();
    console.log(op);

    const hash = await op.confirmation(3);
    console.log(hash);
}

async function main() {
    // await signMsg();

    await offChainView("KT1GWCxfBQvDN1oiFPVQNadS7Mqe3LuAWZ3L");

    // await callContract();
}

main()
    .then(() => process.exit(0));
