import { Component, OnInit } from '@angular/core';
import { sortBy as _sortBy } from 'lodash';
import * as moment from 'moment';

@Component({
  selector: 'app-goal-comments',
  templateUrl: './goal-comments.component.html',
  styleUrls: ['./goal-comments.component.scss'],
})
export class GoalCommentsComponent implements OnInit {


  public data = null;
  public mockData = null;
  public patient = null;
  public goal = null;
  public comments = [];
  public newCommentInput = '';


  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.mockData = this.data.mockData; // Remove eventually
      this.patient = this.data.patient;
      this.goal = this.data.goal;
      this.comments = this.data.goal.comments;
    }
  }

  public orderedComments() {
    if (!this.comments || this.comments.length === 0) {
      return [];
    }
    return _sortBy(this.comments, (obj) => {
      return obj.date;
    });
  }

  public formatDate(date) {
    let oneWeekAgo = moment().add(-6, 'days').startOf('day');
    let startOfToday = moment().startOf('day')
    let tomorrow = moment().add(1, 'days').startOf('day');
    if (date.isBetween(startOfToday, tomorrow)) {
      return 'Today, ' + date.format('hh:mm A');
    } else if (date.isBetween(oneWeekAgo, tomorrow)) {
      return date.format('dddd, hh:mm A');
    } else {
      return date.format('MMM D, hh:mm A');
    }
  }

  public addComment() {
    if (!this.newCommentInput || this.newCommentInput.length === 0) {
      return;
    }
    let goalIndex = this.mockData.goals.findIndex((obj) => obj.id === this.goal.id);
    this.mockData.goals[goalIndex].comments.push({
			id: this.mockData.generateRandomId(),
			date: moment(),
			is_employee: true,
			employee: this.mockData.employees[0],
			text: this.newCommentInput,
		});
    this.newCommentInput = '';
  }
}
