import { Component, OnInit } from '@angular/core';
import { sortBy as _sortBy } from 'lodash';
import * as moment from 'moment';
import { StoreService } from '../../../../../services';

@Component({
  selector: 'app-goal-comments',
  templateUrl: './goal-comments.component.html',
  styleUrls: ['./goal-comments.component.scss'],
})
export class GoalCommentsComponent implements OnInit {


  public data = null;
  public user = null;
  public patient = null;
  public goal = null;
  public comments = [];
  public newCommentInput = '';


  constructor(
    private store: StoreService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.user = this.data.user;
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
      return obj.created;
    });
  }

  public formatDate(date) {
    let dateMoment = moment(date);
    let oneWeekAgo = moment().add(-6, 'days').startOf('day');
    let startOfToday = moment().startOf('day')
    let tomorrow = moment().add(1, 'days').startOf('day');
    if (dateMoment.isBetween(startOfToday, tomorrow)) {
      return 'Today, ' + dateMoment.format('hh:mm A');
    } else if (dateMoment.isBetween(oneWeekAgo, tomorrow)) {
      return dateMoment.format('dddd, hh:mm A');
    } else {
      return dateMoment.format('MMM D, hh:mm A');
    }
  }

  public addComment() {
    if (!this.newCommentInput || this.newCommentInput.length === 0) {
      return;
    }
    this.store.GoalComment.create({
      goal: this.goal.id,
      user: this.user.id,
      content: this.newCommentInput,
    }).subscribe((newComment) => {
      this.comments.push(newComment);
      this.newCommentInput = '';
    });
  }
}
