// src/SearchBar.tsx
import React, { useState, ChangeEvent, KeyboardEvent } from 'react';

const SearchBar: React.FC = () => {
  const [query, setQuery] = useState<string>('');

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      console.log(query); // Print the current input value to the console when Enter is pressed
    }
  };

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        onKeyDown={handleKeyDown} // Add the onKeyDown event handler
        placeholder="Search..."
      />
    </div>
  );
};

export default SearchBar;
