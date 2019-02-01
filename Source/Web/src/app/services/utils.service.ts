import { Injectable } from '@angular/core';
import * as moment from 'moment';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor() { }

  public timePillColor(minutes, allotted) {
    const daysThisMonth = moment().daysInMonth();
    const currentDay = moment().date();

    const test = (currentDay / daysThisMonth) * allotted;

    const greenLimit = test * .9;
    const yellowLimit = test * .7;
    const redLimit = test * .5;

    if (minutes >= greenLimit) {
      return 'pill--lime';
    } else if (minutes >= yellowLimit) {
      return 'pill--yellow';
    } else if (minutes >= redLimit) {
      return 'pill--red';
    } else {
      return 'pill--purple';
    }
  }

  public percentPillColor(percentage) {
    if (percentage >= 90) {
      return '#4caf50';
    } else if (percentage <= 89 && percentage >= 70) {
      return '#ff9800';
    } else if (percentage <= 69 && percentage >= 50) {
       return '#ca2c4e';
    } else {
      return '#880e4f';
    }
  }

  public pillColorStatus(status) {
    if (status === 'done') {
      return '#4caf50';
    } else if (status === 'late') {
       return '#ca2c4e';
    } else if (status === 'missed') {
      return '#880e4f';
    } else if (status === 'open') {
      return '#2180a0';
    }
  }

  public getRiskLevelText(riskLevel) {
    if (riskLevel >= 90) {
      return 'On Track';
    } else if (riskLevel <= 89 && riskLevel >= 70) {
      return 'Low Risk';
    } else if (riskLevel <= 69 && riskLevel >= 50) {
       return 'Med Risk';
    } else {
      return 'High Risk';
    }
  }
}
