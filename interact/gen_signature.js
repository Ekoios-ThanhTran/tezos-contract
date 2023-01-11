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

async function offChainView() {
    const Tezos = new TezosToolkit('https://ghostnet.ecadinfra.com/');
    Tezos.addExtension(new Tzip16Module());

    const contract = await Tezos.contract.at("KT1BQSrroWR3AYUL6Z1brbKF7ikWeN8Eb13P", tzip16);

    // const metadata = await contract.tzip16().getMetadata();

    // console.log(metadata);

    const metadataViews = await contractAbstraction.tzip16().metadataViews();
    // const viewResult = await metadataViews.nameOfTheView().executeView(paramOfTheView);

    console.log(metadataViews)
}

async function signMsg() {
    const signer = await InMemorySigner.fromSecretKey("edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk");

    const formattedInput = [
        // 'Hello World',
        // 'hello',
        0
    ].join(' ');

    // The bytes to sign
    const bytes = char2Bytes(formattedInput);
    // const bytes = char2Bytes('hello');


    console.log(bytes);

    // const bytes = STRING_OF_BYTES;
    const signature = await signer.sign(bytes);

    console.log(signature)
}

async function main() {
    // signMsg();

    await offChainView();
}

main()
    .then(() => process.exit(0));
