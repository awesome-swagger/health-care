import {
  ComponentFactoryResolver,
  ComponentRef,
  Injectable,
  ViewChild,
} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { ModalOutletComponent } from './modal-outlet.component';

export interface DialogPosition {
  type?: string; // Fixed, absolute, relative, etc.
  top?: string;
  bottom?: string;
  left?: string;
  right?: string;
}

@Injectable()
export class ModalService {

  public result: Subject<any> = new Subject();
  private outlet: ModalOutletComponent;

  public optionDefaults = {
    backdropDisabled: true,
    closeDisabled: false,
    height: '',
    width: '',
    minWidth: '',
    animation: 'slideInTop .6s', // scaleIn, slideInTop, etc...
    position: {
      top: '',
    },
    overflowX: '',
    overflowY: '',
    overflow: '',
    data: null,
  };

  constructor(
    private cfr: ComponentFactoryResolver
  ) { }

  public open(type, options = {}) {
    this.result = new Subject();
    let meta = {
      'type': type,
      'options': Object.assign({}, this.optionDefaults, options)
    };
    if (this.outlet.active) {
      this.outlet.active.destroy();
    }
    if (meta.options.position) {
      meta.options.position.top = window.scrollY + 'px';
    }
    let factory = this.cfr.resolveComponentFactory(meta.type);
    this.outlet.active = this.outlet.content.createComponent(factory);
    this.outlet.active.instance.data = meta.options.data;
    this.outlet.options = meta.options;
    this.outlet.visible = true;
    document.querySelector('body').classList.add('noscroll');
    document.querySelector('body').classList.add('relative');
    return this.result;
  }

  public close(data) {
    if (this.outlet.active) {
      this.outlet.active.destroy();
    }
    this.outlet.active = null;
    this.outlet.visible = false;
    document.querySelector('body').classList.remove('noscroll');
    document.querySelector('body').classList.remove('relative');
    this.result.next(data);
    this.result.complete();
  }

  public setOutlet(_outlet) {
    this.outlet = _outlet;
  }
}
