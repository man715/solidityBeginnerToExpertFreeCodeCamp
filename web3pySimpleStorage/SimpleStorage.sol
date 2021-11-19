pragma solidity 0.6.0;

contract SimpleStorage {
    struct Person {
        uint256 favoriteNumber;
        string name;
    }

    uint256 internal favoriteNumber;

    function store (uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    function addIt() public view returns(uint256) {
        return favoriteNumber + favoriteNumber;
    }

    function addNumbers(uint256 a, uint256 b) public view returns(uint256) {
        return a + b;
    }

    Person[] public people;
    mapping(string => uint256) nameToFavoriteNumber;

    function addPeople(string memory _name, uint256 _favoriteNumber) public {
        people.push(Person({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
