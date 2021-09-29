import React from 'react';
import {Route,Switch} from 'react-router-dom';
import Dashboard from './containers/Dashboard'
import ProductPage from './containers/ProductPage';

const BaseRouter = ()=>(
    <Switch>
        <Route  path='/:productID' component={ProductPage}/>
    </Switch>
)

export default BaseRouter;