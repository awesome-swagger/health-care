import { Component, ViewChild, ViewContainerRef, ComponentRef } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { ModalService } from './modal.service';

@Component({
  selector: 'app-modal-outlet',
  templateUrl: './modal-outlet.component.html',
  styleUrls: ['./modal-outlet.component.scss']
})
export class ModalOutletComponent {

  @ViewChild('content', { read: ViewContainerRef })
  public content;

  public active: ComponentRef<any>;

  public visible = false;
  public options: any = {};

  constructor(public modals: ModalService) {
    this.modals.setOutlet(this);
  }

  public close() {
    this.modals.close(null);
  }
}
