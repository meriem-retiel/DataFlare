import React from 'react';
import {Route} from 'react-router-dom';
import Dashboard from './containers/Dashboard'

const BaseRouter = ()=>(
    <div>
        <Route exact path='/' component={Dashboard}/>
        <Route exact path='/:articleID' component={Dashboard}/>
    </div>
)

export default BaseRouter;