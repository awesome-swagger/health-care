import { environment } from '../environments/environment';
import { Utils } from './utils';

export class AppConfig {

  constructor() {
    if (!Utils.isNullOrUndefined(environment.minimumLoggingLevel)) {
      Utils.minimumLoggingLevel = environment.minimumLoggingLevel;
    }
  }

  public static baseUrl = environment.apiHost;
  public static apiUrl = AppConfig.createUrl('api');
  public static restAuthUrl = AppConfig.createUrl('rest-auth');
  public static authTokenUrl = AppConfig.createUrl('api-token-auth');
  public static resetPasswordUrl = AppConfig.createUrl('rest-auth/password/reset');

  public static createUrl(str: string): string {
    return `${this.baseUrl}/${str}/`;
  }

  public static createWithApiUrl(str: string): string {
    return `${this.baseUrl}/api/${str}/`;
  }
}
