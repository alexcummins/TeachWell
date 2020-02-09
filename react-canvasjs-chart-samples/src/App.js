import React, { Component } from 'react';
import Template from './views/Template';
import PieChart from "./views/pie & funnel charts/Pie Chart";
import {Button, ButtonToolbar} from "react-bootstrap";
import LineChart from "./views/line charts/Line Chart";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            line: false
        }
        this.line.bind(this);
    }

    line(){
       this.setState({line: !this.state.line})
    }
  render() {
      if (!this.state.line) {
          return ( <div>
              <div>
                  <Button onClick={() => {this.line()}} > Summary
                  </Button>
              </div>
              <div>


                  <PieChart/>
              </div>
          </div>)

      }
    return (
        <div>
        <div>
        <Button onClick={() => {this.line()}} > Reset
            </Button>
        </div>
        <div>


		<LineChart/>
        </div>
        </div>
    );
  }
}

export default App;
