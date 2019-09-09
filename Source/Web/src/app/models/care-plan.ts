import { MomentInput } from 'moment';

import { IEmployee } from './employee';
import { IHaveId } from './ihaveid';
import { IServiceArea } from './service-area';

export interface ICarePlan extends IHaveId {
  careTeam?: Array<IEmployee>;
  created?: MomentInput;
  duration_weeks?: number;
  is_active?: boolean;
  modified?: MomentInput;
  name?: string;
  service_area?: IServiceArea;
}
