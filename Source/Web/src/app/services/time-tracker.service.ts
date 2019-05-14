import { Injectable, EventEmitter } from '@angular/core';
import { SessionStorageService } from './storage.service';
import { StoreService } from './store.service';

@Injectable()
export class TimeTrackerService {

  public planTimers = {};
  public timer = null;

  public emitBilledActivity = new EventEmitter<any>();

  constructor(
    private session: SessionStorageService,
    private store: StoreService,
  ) {
    let planTimersExist = !!this.session.getObj('planTimers');
    if (planTimersExist) {
      this.planTimers = this.session.getObj('planTimers');
    }
  }

  public createRecord(user, plan) {
    let createSub = this.store.BilledActivity.create({
      plan: plan.id,
      members: [user.id],
      added_by: user.id,
      time_spent: 3,
    }).subscribe(
      (record) => {
        this.emitBilledActivity.next(record);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public startTimer(user, plan) {
    this.stopTimer();
    let billingType = plan.billing_type;
    let isQualified = user.qualified_practitioner;
    // if plan is RPM, only start timer if user is a qualified practitioner
    if (billingType === 'RPM' && !isQualified) {
      return;
    }
    this.timer = setInterval(() => {
      if (!this.planTimers[plan.id]) {
        this.planTimers[plan.id] = 0;
      }
      this.planTimers[plan.id]++;
      if (this.planTimers[plan.id] >= 180) {
        this.createRecord(user, plan);
        this.planTimers[plan.id] = 0;
      }
      this.session.setObj('planTimers', this.planTimers);
    }, 1000);
  }

  public stopTimer() {
    if (!this.timer) return;
    clearInterval(this.timer);
    this.timer = null;
  }

  public resetTimers() {
    this.planTimers = {};
  }
}
