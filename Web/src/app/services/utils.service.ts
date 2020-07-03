import { Injectable } from '@angular/core';
import * as moment from 'moment';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor() { }

  public timePillColorTCM(planStart: moment.MomentInput): string {
    let planStartMoment = moment(planStart);
    let daysSinceStart = moment().diff(planStartMoment, 'days');
    if (daysSinceStart < 7) {
      return 'pill--lime';
    } else if (daysSinceStart < 14) {
      return 'pill--yellow';
    } else if (daysSinceStart < 21) {
      return 'pill--red';
    } else if (daysSinceStart < 29) {
      return 'pill--purple';
    } else {
      return null;
    }
  }

  public timePillColor(minutes: number, allotted: number): string {
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

  public percentPillClass(percentage: number): string {
    if (percentage >= 90) {
      return 'pill--lime';
    } else if (percentage <= 89 && percentage >= 70) {
      return 'pill--yellow';
    } else if (percentage <= 69 && percentage >= 50) {
      return 'pill--red';
    } else {
      return 'pill--purple';
    }
  }

  public pillStatusClass(status: string): string {
    if (status === 'done') {
      return 'pill--lime';
    } else if (status === 'late') {
      return 'pill--red';
    } else if (status === 'missed') {
      return 'pill--purple';
    } else if (status === 'open') {
      return 'pill--blue';
    }
  }

  public getRiskLevelText(riskLevel: number): string {
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
