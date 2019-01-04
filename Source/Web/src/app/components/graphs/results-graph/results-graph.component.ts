import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { get as _get } from 'lodash';
import { directiveCreate } from '@angular/core/src/render3/instructions';

@Component({
  selector: 'app-results-graph',
  templateUrl: './results-graph.component.html',
  styleUrls: ['./results-graph.component.scss']
})
export class ResultsGraphComponent implements OnInit {

  constructor() { }

  ngOnInit() {

    interface WeekData {
      engagement: number,
      outcome: number
    }

    const weeks = [
      { engagement: 100, outcome: 72 },
      { engagement: 90, outcome: 76 },
      { engagement: 85, outcome: 83 },
      { engagement: 93, outcome: 89 },
      { engagement: 90, outcome: 80 },
    ];

    const percentageZones = [
      [-5, 45],
      [45, 70],
      [70, 90],
      [90, 105],
    ];
    const percentageColors = [
      '#880e4f',
      '#ca2c4e',
      '#f1a949',
      '#6db744',
    ]

    const margin = {top: 30, right: 20, bottom: 30, left: 50};
    const width = 1000 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const wrapper = d3.select('#results-graph-wrapper');

    const x = d3.scaleLinear()
      .range([0, width])
      .domain([.8, weeks.length + .2]);
    const y = d3.scaleLinear()
      .range([height, 0])
      .domain([-5, 105]);

    const xAxis = d3.axisBottom(x)
      .ticks(weeks.length)
      .tickSize(0)
      .tickFormat(t => `Week ${t}`)

    const yAxis = d3.axisLeft(y)
      .ticks(5)
      .tickSize(-width)
      .tickFormat(t => `${t}%`)

    const svg = wrapper.append('svg')
      .attr('height', 500)
      .attr('width', 1000)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    const defs = svg.append('defs');
    const linearGradients = defs.selectAll('percent-gradient')
      .data(percentageZones)
      .enter().append('linearGradient')
        .attr('id', (d, i) => `grad${i + 1}`)
        .attr('x1', 0).attr('x2', 0).attr('y1', 0).attr('y2', 1)

    linearGradients.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', (d, i) => percentageColors[i])

    linearGradients.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', (d, i) => percentageColors[i])
      .attr('stop-opacity', .4)

    svg.selectAll('percent-zone')
      .data(percentageZones)
      .enter().append('rect')
        .attr('x', 0)
        .attr('y', (d) => y(d[1]))
        .attr('height', d => height - y(d[1] - d[0] -5))
        .attr('width', width)
        .attr('fill', (d, i) => `url(#grad${i + 1})`)
        .attr('stroke-width', 1)
        .attr('test', (d) => `${d[1] - d[0]}`)

    svg.append('g')
      .attr('transform', `translate(0, ${height})`)
      .attr('class', 'axis')
      .call(xAxis)

    svg.append('g')
      .attr('class', 'axis')
      .call(yAxis);

    const engagementValueLine = d3.line<WeekData>()
      .x((d: WeekData, i) => x(i + 1))
      .y((d: WeekData, i) => y(d.engagement))
      .curve(d3.curveCardinal)

    const outcomeValueLine = d3.line<WeekData>()
      .x((d: WeekData, i) => x(i + 1))
      .y((d: WeekData, i) => y(d.outcome))
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
      .attr('d', engagementValueLine(weeks))
      .attr('stroke-opacity', .75)
      .style('stroke', '#ffffff')
      .style('fill', 'none')
      .style('stroke-width', 3)
      .style('stroke-dasharray', '3, 3')

    svg.selectAll('dot')
      .data(weeks)
      .enter().append('circle')
        .attr('r', 5)
        .attr('cx', (d, i) => x(i + 1))
        .attr('cy', (d) => y(d.engagement))
        .attr('fill', '#ffffff')
        .on('mouseover', (d, i) => {
          tooltip.transition()
            .duration(200)
            .style('opacity', 1)
          tooltip.html(
              `<h4>Week ${i + 1}</h4><span>&middot;&middot;&middot;  Engagement: ${d.engagement}%<br/>&mdash;  Outcome: ${d.outcome}%</span>`
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
      .attr('d', outcomeValueLine(weeks))
      .attr('stroke-opacity', .5)
      .style('stroke', '#ffffff')
      .style('fill', 'none')
      .style('stroke-width', 3)

    svg.selectAll('dot')
      .data(weeks)
      .enter().append('circle')
        .attr('r', 5)
        .attr('cx', (d, i) => x(i + 1))
        .attr('cy', (d) => y(d.outcome))
        .attr('fill', '#ffffff')
        .on('mouseover', (d, i) => {
          tooltip.transition()
            .duration(200)
            .style('opacity', 1)
          tooltip.html(
              `<h4>Week ${i + 1}</h4><span>&middot;&middot;&middot;  Engagement: ${d.engagement}%<br/>&mdash;  Outcome: ${d.outcome}%</span>`
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
