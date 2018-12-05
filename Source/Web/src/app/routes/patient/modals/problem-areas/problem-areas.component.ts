import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';

@Component({
  selector: 'app-problem-areas',
  templateUrl: './problem-areas.component.html',
  styleUrls: ['./problem-areas.component.scss'],
})
export class ProblemAreasComponent implements OnInit {

  public data = null;

  public problemAreas = [
    {
      identifiedDate: 'Mar 17, 2018',
      identifiedBy: 'Lori Ramirez, RN',
      name: 'Severe Depression',
      description: 'Unable to concentrate or keep a job or relationship. Patient stays at home most of the time and does not have a lot of human interaction.',
    },
    {
      identifiedDate: 'Dec 10, 2017',
      identifiedBy: 'Jason Stoneman, MD',
      name: 'Family Issues',
      description: 'Going through a divorce.',
    }
  ]

  public editIndex = -1;
  public deleteIndex = -1;
  public currentEditName = '';
  public currentEditText = '';
  public currentAddName = '';
  public currentAddText = '';

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

  public addProblemArea() {
    this.problemAreas.push({
      identifiedDate: moment().format('MMM DD, YYYY'),
      identifiedBy: this.data && this.data.currentUser,
      name: this.currentAddName,
      description: this.currentAddText,
    })
  }

}
