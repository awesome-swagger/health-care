import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ActivePatientsGraphComponent } from './active-patients-graph.component';

describe('ActivePatientsGraphComponent', () => {
  let component: ActivePatientsGraphComponent;
  let fixture: ComponentFixture<ActivePatientsGraphComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ActivePatientsGraphComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ActivePatientsGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
