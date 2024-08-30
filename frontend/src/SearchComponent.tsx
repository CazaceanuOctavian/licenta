import React, { useEffect, useState } from "react";

interface SearchProps {
    userQuery: string;
    setUserQuery: (query: string) => void;
}

const Search: React.FC<SearchProps> = ({ userQuery, setUserQuery }) => {
    const [query, setQuery] = useState<string>('')

    useEffect(() => {
        window.addEventListener('keydown', handleKeyPress);
                return () => {
          window.removeEventListener('keydown', handleKeyPress);
        };
      }, []); 

      function getStringOrDefault(value: string | null): string {
        return value !== null ? value : "";
    }

    const handleKeyPress = (event: KeyboardEvent) => {
        if(event.key === "Enter"){
            var search = document.getElementById('search_bar') as HTMLInputElement;
            if(search){
                let userQuery:string = getStringOrDefault(search.value)
                setUserQuery(userQuery)
            }
        }
      };

    return (
        <div>
            <input id="search_bar"
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                
                placeholder="Enter your query and press Enter"
            />
        </div>
    )
}

export default Search;
