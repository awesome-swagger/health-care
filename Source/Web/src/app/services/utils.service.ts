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

}
