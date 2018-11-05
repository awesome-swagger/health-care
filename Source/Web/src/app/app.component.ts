import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Router, NavigationError, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import 'rxjs/add/operator/filter';
import { NavComponent } from './components';
import { NavbarService } from './services/';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {

  @ViewChild('navbar')
  public navbar: NavComponent;

  private routerSub: Subscription;
  private dataSub: Subscription;

  constructor(
    private router: Router,
    private title: Title,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    let routerSub = this.router.events
      .filter(event => event instanceof NavigationEnd)
      .subscribe(event => {
        // scroll to top on route change
        window.scrollTo(0, 0);
        // change browser tab/window title on route change
        this.dataSub = this.router.routerState.root.firstChild.data.subscribe((data: any) => {
          let titleStr = data.title || this.router.routerState.root.firstChild.routeConfig.path;
          this.setTitle(titleStr);
        });
        // Set navbar to visible
        this.nav.instance = this.navbar;
        this.nav.show();
        this.nav.normalState();
        if (this.nav.instance) {
          this.nav.instance.closeAllPopovers();
        }
      });
  }

  public ngOnDestroy() {
    this.routerSub.unsubscribe();
    this.dataSub.unsubscribe();
  }

  private setTitle(moreTitle: string) {
    let title = 'CareAdopt';
    if (moreTitle) {
      title += ` | ${moreTitle}`;
    }
    this.title.setTitle(title);
  }
}
