import React, { Component } from 'react';
import {Helmet} from 'react-helmet'
import CanvasJSReact from '../../assets/canvasjs.react';
import axios from 'axios';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 
class PieChart extends Component {

	constructor(props) {
		super(props);
		this.state = {
			data: {
				"e": 0,
				"ne": 0,
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
		const bgcolor = 						this.state.data.e >= 60 ? '#90ee90'
			: this.state.data.ne >= 60 ? 'pink'
				: '#ffffba';
		const options = {
			backgroundColor: bgcolor,
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
					{ y: this.state.data.e, label: "Engaged", color: "green" },
					{ y: this.state.data.ne, label: "Not engaged"  },
				]
			}],
			width:window.innerWidth,
			height:window.innerHeight-50,
		}

		return (
		<div>
			<CanvasJSChart options = {options} 
				onRef={ref => this.chart = ref}
			/>
			{/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
		</div>
		);
	}
}

export default PieChart;