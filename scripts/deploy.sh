export RPC=https://ghostnet.ecadinfra.com/
# export RPC=https://ghostnet.smartpy.io

export PK=edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk

# curl https://ghostnet.ecadinfra.com/chains/main/blocks/head/context/contracts/KT1EZjdjzH7foZgGFywHJtS7Dak7tF5gBVD6/storage

# curl https://ghostnet.smartpy.io/chains/main/blocks/head/context/contracts/KT1G75nancCqe7xA9SuUjwFVgomAGyqciWL3/storage

# ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/barterContract/barter/step_000_cont_0_contract.tz --storage output/contracts/barterContract/barter/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK

# ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/checkSignature/testChecksignature/step_000_cont_0_contract.tz --storage output/contracts/checkSignature/testChecksignature/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK

# ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/stringUtils/stringManipulations/step_000_cont_0_contract.tz --storage output/contracts/stringUtils/stringManipulations/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK

~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/fa2Contract/FA2/step_000_cont_0_contract.tz --storage output/contracts/fa2Contract/FA2/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK

# pwd