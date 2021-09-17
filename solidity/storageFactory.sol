// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "./simpleStorage.sol";

// contract storageFactory is simpleStorage{

contract storageFactory{

    simpleStorage[] public simpleStorageArray;
    
    function createSimpleStorageContract() public{
        simpleStorage SimpleStorage = new simpleStorage();
        simpleStorageArray.push(SimpleStorage);
    }
    
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public{
        // address
        // ABI - Application Binary Interface
        
        // simpleStorage SimpleStorage= simpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        // SimpleStorage.store(_simpleStorageNumber);
        simpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(_simpleStorageNumber);
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256){
        // simpleStorage SimpleStorage = simpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        // return SimpleStorage.retrieve();
        return simpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve();
    }
}
