import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-percentage-gauge',
  templateUrl: './percentage-gauge.component.html',
  styleUrls: ['./percentage-gauge.component.scss']
})
export class PercentageGaugeComponent implements OnInit {
  @ViewChild('chart')
  private chartContainer: ElementRef;
  private _percent = 0;
  private _size = 196;

  @Input()
  public get percent(): number {
    return this._percent;
  }

  public set percent(percent: number) {
    this._percent = percent;
    this.drawChart();
  }

  @Input()
  public get size(): number {
    return this._size;
  }

  public set size(size: number) {
    this._size = size;
  }

  ngOnInit(): void {
    this.drawChart();
  }

  private drawChart(): void {
    const percent = this.percent || 0;
    const half = this.size / 2;
    const trackWidth = 15;
    const trackColor = '#45555a'
    const endAngle = Math.PI * 2;
    const textColor = '#ffffff';
    const element = this.chartContainer.nativeElement;
    element.innerHTML = '';

    const wrapper = d3.select(element);
    const circle = d3.arc()
      .startAngle(0)
      .innerRadius(half - trackWidth)
      .outerRadius(half);
    const svg = wrapper.append('svg')
      .attr('width', this.size)
      .attr('height', this.size);
    const g = svg.append('g')
      .attr('transform', `translate(${half}, ${half})`);

    const track = g.append('g')
      .attr('class', 'radial-progress');

    track.append('path')
      .attr('class', 'radial-progress__background')
      .attr('fill', trackColor)
      .attr('stroke-width', trackWidth)
      .attr('d', circle.endAngle(endAngle));

    track.append('path')
      .attr('class', 'radial-progress__value')
      .attr('fill', this.color)
      .attr('stroke-width', trackWidth)
      .attr('d', circle.endAngle(endAngle * (percent / 100)));

    track.append('text')
      .attr('class', 'radial-progress__text')
      .attr('fill', textColor)
      .attr('text-anchor', 'middle')
      .attr('dy', '.5rem')
      .style('font-size', '3rem')
      .style('font-weight', 100)
      .text(`${percent || 0}%`);
  }

  private get color(): string {
    if (this.percent >= 90) {
      return '#4caf50';
    }

    if (this.percent >= 70) {
      return '#ff9800';
    }

    if (this.percent >= 50) {
      return '#f44336';
    }

    return '#880e4f';
  }
}

