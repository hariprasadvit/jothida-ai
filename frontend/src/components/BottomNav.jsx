import { NavLink } from 'react-router-dom';
import { Home, Heart, Sparkles, BookOpen, User } from 'lucide-react';

const navItems = [
  { path: '/dashboard', icon: Home, label: 'முகப்பு' },
  { path: '/matching', icon: Heart, label: 'பொருத்தம்' },
  { path: '/chat', icon: Sparkles, label: 'ஜோதிடம்' },
  { path: '/stories', icon: BookOpen, label: 'கதைகள்' },
  { path: '/profile', icon: User, label: 'சுயவிவரம்' },
];

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-orange-200 shadow-lg safe-bottom">
      <div className="flex justify-around items-center h-16 max-w-lg mx-auto">
        {navItems.map(({ path, icon: Icon, label }) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              `flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-all border ${
                isActive
                  ? 'bg-orange-50 border-orange-200 text-orange-600'
                  : 'border-transparent text-gray-400 hover:text-gray-600 hover:bg-orange-50/40'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <div className={`p-1.5 rounded-full ${isActive ? 'bg-orange-100' : ''}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className="text-xs">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
