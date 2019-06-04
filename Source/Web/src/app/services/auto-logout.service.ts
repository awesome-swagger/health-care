import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { TimeTrackerService } from './time-tracker.service';
import store from 'store';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AutoLogoutService {

  constructor(
    private auth: AuthService,
    private timer: TimeTrackerService,
    private router: Router,
  ) {
    this.initClickListener();
    this.initInterval();
  }

  get lastAction() {
    return store.get('lastAction');
  }

  set lastAction(value) {
    store.set('lastAction', value);
  }

  private initClickListener() {
    document.body.addEventListener('click', () => this.reset())
  }

  private initInterval() {
    setInterval(() => {
      this.checkInactiveTime();
    }, 30000)
  }

  private reset() {
    this.lastAction = Date.now();
  }

  private checkInactiveTime() {
    const now = Date.now();
    const timeLeft = parseInt(this.lastAction) + 1800000;
    const diff = timeLeft - now;

    if (diff < 0 && this.auth.isLoggedIn()) {
      console.log('logging out');
      this.timer.stopTimer();
      this.timer.resetTimers();
      this.auth.logout();
      this.router.navigate(['login']);
      window.location.reload();
    }
  }
}
