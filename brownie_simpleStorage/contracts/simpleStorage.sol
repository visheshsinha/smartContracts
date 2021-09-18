// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract simpleStorage{
    
    uint256 favNumber;
    address myAddress = 0x73BEc69aC0fA10534Ad56333C5c8697D365C535a;
    
    struct People {
        uint256 favNumber;
        string name;
    }
    
    // People public person = People({favNumber: 2, name: "Vishesh"});
    
    People[] public people;
    mapping(string => uint256) public nameTofavNumber;
    
    function store(uint256 _favNumber) public {
        favNumber = _favNumber;
    }
    
    function retrieve() public view returns(uint256){
        return favNumber;
    }
    
    function addPerson(string memory _name, uint256 _favNumber) public{
        people.push(People(_favNumber, _name));
        nameTofavNumber[_name] = _favNumber;
    }
}
