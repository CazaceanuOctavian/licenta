import FetchAndPopulate from './FetchAndPopulate'
import SearchBar from './Searchbar';

function App() {
  return (
    <p className=''>
          <SearchBar></SearchBar>
          <p className = 'products-list'>{FetchAndPopulate('samsung galaxy smartwatch')}</p>
    </p>
  )
}

export default App;