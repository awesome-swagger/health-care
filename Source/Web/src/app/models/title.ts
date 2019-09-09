import { IHaveId } from "./ihaveid";

export interface ITitle extends IHaveId {
  abbreviation?: string;
  name?: string;
}

//export class Title {
//	abbreviation: string;
//	id: string;
//	name: string;
//}
