import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { AppModule } from '../../../app.module';
import { PlanScheduleComponent } from './schedule.component';

describe('PlanScheduleComponent', () => {
  let component: PlanScheduleComponent;
  let fixture: ComponentFixture<PlanScheduleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        AppModule
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlanScheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
