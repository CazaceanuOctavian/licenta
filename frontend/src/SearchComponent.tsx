import React, { useState } from "react";

interface SearchProps {
    userQuery: string;
    setUserQuery: (query: string) => void;
}

const Search: React.FC<SearchProps> = ({ userQuery, setUserQuery }) => {
    const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            console.log(userQuery);
        }
    }
    // const handlesubmit = (event: React.FormEvent<HTMLFormElement>) => {
    //     event.preventDefault();
    //     if
    //   };

    return (
        <div>
            <input id="search_bar"
                type="text"
                value={userQuery}
                onKeyDown={handleKeyPress}
                onChange={(e) => setUserQuery(e.target.value)}
                
                placeholder="Enter your query and press Enter"
            />
        </div>
    )
}

export default Search;
