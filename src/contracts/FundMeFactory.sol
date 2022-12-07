// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;
    uint256 public entranceFeeUSD;

    constructor(address _owner, address _priceFeed, uint256 _minEntranceFeeUSD) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = _owner;
        entranceFeeUSD = _minEntranceFeeUSD;
    }

    function getDecimals() public view returns (uint8) {
        return priceFeed.decimals();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    // Enter with a amount of ETH (in Wei - 18 decimal points). return the amount in dolar (in Wei - 18 decomal points)
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10**18;
        return ethAmountInUsd;
    }

    function convertEntranceFee(uint256 entranceFeeETH) public view returns (uint256) {
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return ((entranceFeeETH * price) / precision);
    }

    function fund() public payable {
        require(convertEntranceFee(msg.value) >= entranceFeeUSD, "You need to spend more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }


    function withDraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}

contract FundMeFactory {
    FundMe[] public FundmeArray;
    address public factoryDeployer;

    constructor() public {
        factoryDeployer = msg.sender;
    }

    function createFundMeContract(address _owner, address _priceFeed, uint256 _minEntranceFeeUSD) public returns (address) {
        FundMe fundme = new FundMe(_owner, _priceFeed, _minEntranceFeeUSD);
        FundmeArray.push(fundme);
        return address(fundme);
    }

    function getFund(uint256 _fundmeIndex) public view returns (uint256) {
        return FundMe(address(FundmeArray[_fundmeIndex])).getPrice();
    }

}