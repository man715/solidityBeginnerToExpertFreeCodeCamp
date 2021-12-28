// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    // store all palyers
    address payable[] public players;
    // store recent winner
    address payable public recentWinner;
    // recent random number
    uint256 public recentRandomNumber;
    // the minimal entry fee in USD in Wei format (18 decimals)
    uint256 public usdEntryFee;
    // state of the lottery
    enum LotteryState {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LotteryState public lotteryState;
    AggregatorV3Interface internal ethUsdPriceFeed;
    uint256 public fee; // required by the VRFCoordinator
    bytes32 public keyhash; // VRFCoordinator
    // create a new type of an event
    event RequestedRandomness(bytes32 requestId);

    // we can add a constructor from an imported contract
    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator, // required by VRFConsumer
        address _link, // required by VRFConsumer
        uint256 _fee, // VRFConsumer
        bytes32 _keyhash // VRFConsumer
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        // Entrance fee of 50 USD in Wei format
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lotteryState = LotteryState.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lotteryState == LotteryState.OPEN);
        // minimum 50 USD
        // require what is sent is greater than or equal to the entrance fee
        require(msg.value >= getEntranceFee(), "Not enough ETH");
        // record the player
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        // this will return a price that is 8 decimal places
        // https://docs.chain.link/docs/ethereum-addresses/
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        // convert to an uint256 and get it into Wei format of 18 decimals
        uint256 adjustedPrice = uint256(price) * 10**10;

        // we need to add an additiona 10**18 to
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lotteryState == LotteryState.CLOSED,
            "Can't start a new lottery yet."
        );
        lotteryState = LotteryState.OPEN;
    }

    function endLottery() public onlyOwner {
        lotteryState = LotteryState.CALCULATING_WINNER;

        // get random number
        // get the request ID
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    // this function is called by the VRFConsumerBase contract
    // and it gives us the random number
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lotteryState == LotteryState.CALCULATING_WINNER,
            "You are not there yet"
        );
        require(_randomness > 0, "Random not Found");
        recentRandomNumber = _randomness;
        recentWinner = players[_randomness % players.length];
        recentWinner.transfer(address(this).balance);

        // reset
        players = new address payable[](0);
        lotteryState = LotteryState.CLOSED;
    }
}
