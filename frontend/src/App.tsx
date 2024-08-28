import React, { useState } from 'react';
import FetchAndPopulate from './FetchAndPopulate';
import SearchBar from './Searchbar';

function App() {
  const [query, setQuery] = useState<string>('telefon');

  const handleQueryChange = (newQuery: string) => {
    setQuery(newQuery);
  };

  const handleSearch = () => {
    console.log(query); 
  };

  return (
      <div className='products-list'>
        <FetchAndPopulate />
      </div>
  );
}

export default App;
