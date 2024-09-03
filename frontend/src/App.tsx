import React from 'react';
import { Home } from './PathComponents/HomeComponent';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Products from './PathComponents/ProductsComponent';
import ProductDetailsComponent from './PathComponents/ProductDetailsComponent';

const App: React.FC = () => {

  
  return (
    <Router>
      <Routes>
        <Route path='/' Component={Home}></Route>
        <Route path='products/search/' Component={Products}></Route>
        <Route path='products/current_product/:productId' Component={ProductDetailsComponent}></Route>
      </Routes>
    </Router>
  );
}

export default App;
