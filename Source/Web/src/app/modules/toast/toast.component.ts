import { Component, OnInit } from '@angular/core';
import {
  trigger,
  state,
  style,
  animate,
  transition
} from '@angular/animations';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { ToastService, Toast as ToastInterface } from './toast.service';

@Component({
  selector: 'app-toast-outlet',
  template: `
    <ul class="toasts">
      <li class="toast toast--{{toast.type}}" *ngFor="let toast of toasts | async; let i = index"
      [@appear] (click)="close(toast.id, i); route(toast);">
        <div class="toast__text">{{toast.text}}</div>
        <div class="toast__close" *ngIf="toast.closeButton"><i class="ss-delete"></i></div>
      </li>
    </ul>
  `,
  styleUrls: ['./toast.component.scss'],
  animations: [
    trigger('appear', [
      state('void', style({ opacity: 0, transform: "translateY(64px)" })),
      state('*', style({ opacity: 1, transform: "translateY(0)" })),
      transition('void <=> *', [
        animate(200)
      ]),
    ])
  ],
})
export class ToastComponent implements OnInit {

  public toasts: Observable<Array<ToastInterface>>;

  constructor(
    private toast: ToastService,
    private router: Router,
  ) { }

  public ngOnInit() {
    this.toasts = this.toast.toasts$;
  }

  public route(toast) {
    if (toast.internalLink) {
      this.router.navigate(toast.internalLink);
    } else if (toast.externalLink) {
      window.location.assign(toast.externalLink);
    }
  }

  public close(id: number, index?: number) {
    this.toast.remove(id, index);
  }
}
