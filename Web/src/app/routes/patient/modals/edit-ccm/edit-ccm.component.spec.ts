import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditCcmComponent } from './edit-ccm.component';

describe('EditCcmComponent', () => {
  let component: EditCcmComponent;
  let fixture: ComponentFixture<EditCcmComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditCcmComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditCcmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
