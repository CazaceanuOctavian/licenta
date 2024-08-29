import React from 'react';
import FetchAndPopulate from './FetchAndPopulate';
import { Home } from './HomeComponent';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Products from './ProductsComponent';

const App: React.FC = () => {

  
  return (
    <Router>
      <Routes>
        <Route path='/' Component={Home}></Route>
        <Route path='products/search.old/' Component={FetchAndPopulate}></Route>
        <Route path='products/search/' Component={Products}></Route>
      </Routes>
    </Router>

      // <div className='products-list'>
      //   <FetchAndPopulate />
      // </div>
  );
}

export default App;
