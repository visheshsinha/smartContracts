// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract draw is VRFConsumerBase, Ownable {

    address payable[] public users;
    address payable public recentWinner;
    uint256 minUSD;
    uint256 recentRandomness;

    AggregatorV3Interface internal ethUSDpriceFeed;

    enum DRAW_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    DRAW_STATE public draw_state;

    uint256 public fee;
    bytes32 public keyhash;

    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        minUSD = 50 * (10**18);
        ethUSDpriceFeed = AggregatorV3Interface(_priceFeedAddress);
        draw_state = DRAW_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(draw_state == DRAW_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough Tokens !");
        users.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 answer, , , ) = ethUSDpriceFeed.latestRoundData();
        uint256 costEntry = (minUSD * (10**18)) / (uint256(answer) * (10**10));
        return costEntry;
        // return uint256(uint256(answer) * (10**10));
    }

    function startDraw() public onlyOwner {
        require(draw_state == DRAW_STATE.CLOSED, "Draw is Already Running");
        draw_state = DRAW_STATE.OPEN;
    }

    function endDraw() public onlyOwner {
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce,
        //             msg.sender,
        //             block.difficulty,
        //             block.timestamp
        //         )
        //     )
        // ) % users.length;

        draw_state = DRAW_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(draw_state == DRAW_STATE.CALCULATING_WINNER);
        require(_randomness > 0, "No Random Found");

        uint256 indexOfWinner = _randomness % users.length;
        recentWinner = users[indexOfWinner];
        recentRandomness = _randomness;

        recentWinner.transfer(address(this).balance);

        users = new address payable[](0);
        draw_state = DRAW_STATE.CLOSED;
    }
}
