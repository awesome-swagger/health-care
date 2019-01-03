import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import * as d3 from 'd3';
import * as shortid from 'shortid';

@Component({
  selector: 'app-percentage-gauge',
  templateUrl: './percentage-gauge.component.html',
  styleUrls: ['./percentage-gauge.component.scss']
})
export class PercentageGaugeComponent implements OnInit {

  @ViewChild('chart') private chartContainer: ElementRef;
  private _percent = 0;
  private _size = 196;
  public chartId = '';

  constructor() { }

  @Input()
  public get percent() {
    return this._percent;
  }

  public set percent(percent) {
    this._percent = percent;
  }

  @Input()
  public get size() {
    return this._size;
  }
  public  set size(size) {
    this._size = size;
  }

  ngOnInit() {

    this.chartId = shortid.generate();

    const percent = this.percent;
    const trackWidth = 15;
    const trackColor = '#45555a'
    const endAngle = Math.PI * 2;
    const textColor = '#ffffff';

    let element = this.chartContainer.nativeElement;
    let wrapper = d3.select(element);

    let circle = d3.arc()
      .startAngle(0)
      .innerRadius(this.size/2 - trackWidth)
      .outerRadius(this.size/2)

    let svg = wrapper.append('svg')
      .attr('width', this.size)
      .attr('height', this.size)

    let g = svg.append('g')
      .attr('transform', 'translate(' + this.size / 2 + ',' + this.size / 2 + ')');

    let track = g.append('g')
      .attr('class', 'radial-progress');

    track.append('path')
      .attr('class', 'radial-progress__background')
      .attr('fill', trackColor)
      .attr('stroke-width', trackWidth)
      .attr('d', circle.endAngle(endAngle));

    let value = track.append('path')
      .attr('class', 'radial-progress__value')
      .attr('fill', this.color)
      .attr('stroke-width', trackWidth)
      .attr('d', circle.endAngle(endAngle * (percent/100)))

    let numberText = track.append('text')
      .attr('class', 'radial-progress__text')
      .attr('fill', textColor)
      .attr('text-anchor', 'middle')
      .attr('dy', '.5rem')
      .style('font-size', '3rem')
      .style('font-weight', 100)
      .text(`${percent}%`);
  }

  get color() {
    if (this.percent >= 90) {
      return '#4caf50';
    } else if (this.percent >= 70) {
      return '#ff9800';
    } else if (this.percent >= 50) {
      return '#f44336';
    } else {
      return '#880e4f';
    }
  }
}
