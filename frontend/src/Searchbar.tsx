// src/SearchBar.tsx
import React, { ChangeEvent, KeyboardEvent } from 'react';

interface SearchBarProps {
  query: string;
  onQueryChange: (newQuery: string) => void;
  onSearch: () => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ query, onQueryChange, onSearch }) => {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onQueryChange(event.target.value);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      onSearch(); // Trigger the search when Enter is pressed
    }
  };

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder="Search..."
      />
    </div>
  );
};

export default SearchBar;
