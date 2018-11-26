import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllModalsComponent } from './all-modals.component';

describe('AllModalsComponent', () => {
  let component: AllModalsComponent;
  let fixture: ComponentFixture<AllModalsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllModalsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllModalsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
