import { IHaveId } from "./ihaveid";

export interface ITitle extends IHaveId {
  abbreviation?: string;
  name?: string;
}
