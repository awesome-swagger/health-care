import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-error',
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.scss'],
})
export class ErrorComponent implements OnDestroy, OnInit {

  private interval: any;
  public remainingSeconds = 5;

  public constructor(
    private router: Router,
  ) { }

  public ngOnInit() {
    this.countdown();
  }

  public ngOnDestroy() {
    clearInterval(this.interval);
  }

  private countdown() {
    this.interval = setInterval(() => {
      this.remainingSeconds--;
      if (this.remainingSeconds === 0) {
        clearInterval(this.interval);
        this.redirect();
      }
    }, 1000);
  }

  private redirect() {
    this.router.navigate(['/']);
  }
}
