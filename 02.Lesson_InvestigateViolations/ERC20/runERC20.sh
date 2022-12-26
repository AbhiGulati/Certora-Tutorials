SOLC_VERSION=0.8.0 certoraRun ERC20Fixed.sol:ERC20 --verify ERC20:ERC20.spec \
    --optimistic_loop \
    --msg "$1"
