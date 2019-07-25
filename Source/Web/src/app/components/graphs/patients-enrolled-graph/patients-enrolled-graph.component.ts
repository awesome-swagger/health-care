import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import * as d3 from 'd3';
import { map as _map } from 'lodash';

interface MonthData {
  month: string
  enrolled: number
  billable: number
}

@Component({
  selector: 'app-patients-enrolled-graph',
  templateUrl: './patients-enrolled-graph.component.html',
  styleUrls: ['./patients-enrolled-graph.component.scss']
})
export class PatientsEnrolledGraphComponent implements OnInit {
  private _data;
  @Input()
  public get data() {
    return this._data;
  }
  public set data(data) {
    this._data = data;
    this.drawChart();
  }
  @ViewChild('chart')
  private chartContainer: ElementRef;

  ngOnInit() {
    this.drawChart();
  }

  public drawChart() {
    const chartWidth = 1300;
    const months = this._data.reverse();
    const margin = { top: 30, right: 20, bottom: 30, left: 50 };
    const width = chartWidth - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;
    const element = this.chartContainer.nativeElement;
    element.innerHTML = '';
    const wrapper = d3.select(element);

    function getUpperLimit(months) {
      const enrolled = _map(months, m => m.enrolled);
      const billable = _map(months, m => m.billable);
      const values = [...enrolled, ...billable];
      const maxValue = Math.max(...values);
      return Math.ceil(maxValue / 100) * 100;
    }

    const upperLimit = getUpperLimit(months);

    const x = d3.scaleLinear()
      .range([0, width])
      .domain([.8, months.length + .2]);
    const y = d3.scaleLinear()
      .range([height, 0])
      .domain([-5, upperLimit + upperLimit / 20]);

    const xAxis = d3.axisBottom(x)
      .ticks(months.length <= 8 ? months.length : 8)
      .tickSize(0)
      .tickFormat((t: number) => months[t - 1].month)

    const yAxis = d3.axisLeft(y)
      .ticks(5)
      .tickSize(-width)
      .tickFormat(t => `${t}`)

    const svg = wrapper.append('svg')
      .attr('height', 500)
      .attr('width', chartWidth)
      .append("g")
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    svg.append('rect')
      .attr('x', 0)
      .attr('y', 0)
      .attr('height', height)
      .attr('width', width)
      .attr('fill', '#2F3D45')
      .attr('stroke-width', 0)

    svg.append('g')
      .attr('transform', `translate(0, ${height})`)
      .attr('class', 'axis')
      .call(xAxis)

    svg.append('g')
      .attr('class', 'axis')
      .call(yAxis);

    const enrolledValueLine = d3.line<MonthData>()
      .x((d: MonthData, i) => x(i + 1))
      .y((d: MonthData, i) => y(d.enrolled))
      .curve(d3.curveCardinal)

    const billableValueLine = d3.line<MonthData>()
      .x((d: MonthData, i) => x(i + 1))
      .y((d: MonthData, i) => y(d.billable))
      .curve(d3.curveCardinal)

    const tooltip = d3.select('body').append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('opacity', 0)
      .style('color', 'white')
      .style('padding', '10px 20px')
      .style('background', '#45555a')
      .style('border-radius', '5px')

    svg.append('path')
      .attr('class', 'line')
      .attr('d', enrolledValueLine(months))
      .attr('stroke-opacity', .75)
      .style('stroke', '#ffffff')
      .style('fill', 'none')
      .style('stroke-width', 3)
      .style('stroke-dasharray', '3, 3')

    svg.selectAll('dot')
      .data(months)
      .enter().append('circle')
      .attr('r', 5)
      .attr('cx', (d, i) => x(i + 1))
      .attr('cy', (d: MonthData) => y(d.enrolled))
      .attr('fill', '#ffffff')
      .on('mouseover', (d: MonthData, i) => {
        tooltip.transition()
          .duration(200)
          .style('opacity', 1)
        tooltip.html(
          `<h4>${d.month}</h4><span><span style="color: #49b48b">&middot;&middot;&middot;</span>  Enrolled: ${d.enrolled}<br/><span style="color: #49b48b;">&mdash;</span>  Billable: ${d.billable}</span>`
        )
          .style('left', (d3.event.pageX) + "px")
          .style('top', (d3.event.pageY + 30) + "px")
      })
      .on('mouseout', (d) => {
        tooltip.transition()
          .duration(500)
          .style('opacity', 0)
      })

    svg.append('path')
      .attr('d', billableValueLine(months))
      .attr('stroke-opacity', .5)
      .style('stroke', '#49b48b')
      .style('fill', 'none')
      .style('stroke-width', 3)

    svg.selectAll('dot')
      .data(months)
      .enter().append('circle')
      .attr('r', 5)
      .attr('cx', (d, i) => x(i + 1))
      .attr('cy', (d: MonthData) => y(d.billable))
      .attr('fill', '#49b48b')
      .on('mouseover', (d: MonthData, i) => {
        tooltip.transition()
          .duration(200)
          .style('opacity', 1)
        tooltip.html(
          `<h4>${d.month}</h4><span><span style="color: #49b48b;">&middot;&middot;&middot;</span>  Enrolled: ${d.enrolled}<br/><span style="color: #49b48b;">&mdash;</span>  Billable: ${d.billable}</span>`
        )
          .style('left', (d3.event.pageX) + "px")
          .style('top', (d3.event.pageY + 30) + "px")
      })
      .on('mouseout', (d) => {
        tooltip.transition()
          .duration(500)
          .style('opacity', 0)
      })

    d3.selectAll('.axis').selectAll('text')
      .attr('fill', 'white')
      .style('font-size', '14px')
      .style('font-weight', 'bold')

    d3.selectAll('.domain').style('display', 'none')
    d3.selectAll('.axis').selectAll('.tick').selectAll('line')
      .attr('stroke', 'white')
      .attr('fill', 'none')
      .attr('stroke-opacity', .4)

  }
}
