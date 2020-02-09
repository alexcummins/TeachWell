import React, { Component } from 'react';
import CanvasJSReact from '../../assets/canvasjs.react';
import axios from 'axios';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 
class PieChart extends Component {

	constructor(props) {
		super(props);
		this.state = {
			data: {
				"e": 51,
				"ne": 49,
			},
			count: 0
		}
	}

	getData(){
		axios.get('http://localhost:3000/data.json')
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
			exportEnabled: true,
			animationEnabled: true,
			title: {
				text: "Lesson Engagement"
			},
			data: [{
				type: "pie",
				startAngle: 75,
				toolTipContent: "<b>{label}</b>: {y}%",
				showInLegend: "true",
				legendText: "{label}",
				indexLabelFontSize: 16,
				indexLabel: "{label} - {y}%",
				dataPoints: [
					{ y: this.state.data.e, label: "Engaged" },
					{ y: this.state.data.ne, label: "Not engaged" },
				]
			}]
		}

		return (
		<div>
			<h1>React Pie Chart</h1>
			<CanvasJSChart options = {options} 
				onRef={ref => this.chart = ref}
			/>
			{/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
		</div>
		);
	}
}

export default PieChart;