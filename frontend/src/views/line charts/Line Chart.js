import React, { Component } from 'react';
import CanvasJSReact from '../../assets/canvasjs.react';
import axios from "axios";
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 
class LineChart extends Component {

	constructor(props) {
		super(props);
		this.state = {
			data: [],
			count: 0
		}
	}

	getData(){
		axios.get('http://localhost:3000/summaryData.json')
			.then( (response)=> {
				// console.log(response);
				this.setState({data: response.data}).then(() => {
					this.chart.render()
					console.log(JSON.stringify(this.state.data))})
			})
	};

	componentDidMount() {
		setInterval(() => this.getData(), 10000)
	}

	render() {
		const options = {
			animationEnabled: true,
			exportEnabled: true,
			theme: "light2", // "light1", "dark1", "dark2"
			title:{
				text: "Lesson Engagement Over Time"
			},
			axisY: {
				title: "Engagement",
				includeZero: false,
				suffix: "%"
			},
			axisX: {
				title: "Time",
				prefix: "10s",
				interval: 2
			},
			data: [{
				type: "line",
				toolTipContent: "Time {x}: {y}%",
				dataPoints: this.state.data,
				// dataPoints: [
				// 	{ x: 1, y: 64 },
				// 	{ x: 2, y: 61 },
				// 	{ x: 3, y: 64 },
				// 	{ x: 4, y: 62 },
				// 	{ x: 5, y: 64 },
				// 	{ x: 6, y: 60 },
				// 	{ x: 7, y: 58 },
				// 	{ x: 8, y: 59 },
				// 	{ x: 9, y: 53 },
				// 	{ x: 10, y: 54 },
				// 	{ x: 11, y: 61 },
				// 	{ x: 12, y: 60 },
				// 	{ x: 13, y: 55 },
				// 	{ x: 14, y: 60 },
				// 	{ x: 15, y: 56 },
				// 	{ x: 16, y: 60 },
				// 	{ x: 17, y: 59.5 },
				// 	{ x: 18, y: 63 },
				// 	{ x: 19, y: 58 },
				// 	{ x: 20, y: 54 },
				// 	{ x: 21, y: 59 },
				// 	{ x: 22, y: 64 },
				// 	{ x: 23, y: 59 }
				// ]
			}]
		}
		
		return (
		<div>
			<CanvasJSChart options = {options}
				/* onRef={ref => this.chart = ref} */
			/>
			{/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
		</div>
		);
	}
}

export default LineChart;                           