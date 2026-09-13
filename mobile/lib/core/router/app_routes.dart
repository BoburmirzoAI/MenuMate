/// Barcha route path'lari — bir joyda konstantalar.
class AppRoutes {
  AppRoutes._();

  // --- Splash & Onboarding ---
  static const splash = '/';
  static const onboarding = '/onboarding';
  static const languageSelect = '/language';

  // --- Auth ---
  static const login = '/login';
  static const register = '/register';
  static const forgotPassword = '/forgot-password';
  static const resetPassword = '/reset-password';

  // --- Onboarding (post-register) ---
  static const familyCreate = '/family/create';
  static const memberAdd = '/family/members/add';
  static const memberList = '/family/members';

  // --- Main (shell tabs) ---
  static const home = '/home';
  static const menuList = '/menu';
  static const shopping = '/shopping';
  static const recipes = '/recipes';
  static const profile = '/profile';

  // --- Detail'lar ---
  static const menuDetail = '/menu/:id';
  static const dayDetail = '/menu/:id/day/:dayId';
  static const recipeDetail = '/recipes/:id';
  static const changeMeal = '/menu/:id/meals/:mealId/change';
  static const notifications = '/notifications';
  static const settings = '/settings';
}
