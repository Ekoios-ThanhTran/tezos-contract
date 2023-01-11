# export RPC=https://ghostnet.ecadinfra.com/
export RPC=https://ghostnet.smartpy.io

export PK=edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk

# curl https://ghostnet.ecadinfra.com//chains/main/blocks/head/context/contracts/KT1LszVmg96CArHGQg1UkcsbXDFPKtzPD8Ge/storage

# ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/barterContract/barter/step_000_cont_0_contract.tz --storage output/contracts/barterContract/barter/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK

~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/checkSignature/testChecksignature/step_000_cont_0_contract.tz --storage output/contracts/checkSignature/testChecksignature/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK

# pwd