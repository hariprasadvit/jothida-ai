import { BrowserRouter, Routes, Route, useLocation, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Dashboard from './pages/Dashboard';
import Matching from './pages/Matching';
import Chat from './pages/Chat';
import Muhurtham from './pages/Muhurtham';
import Profile from './pages/Profile';
import Onboarding from './pages/Onboarding';
import MobileLogin from './pages/MobileLogin';
import AuthCallback from './pages/AuthCallback';
import CompleteProfile from './pages/CompleteProfile';
import BottomNav from './components/BottomNav';

const queryClient = new QueryClient();

// Protected Route component - redirects to login if not authenticated
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  const hasProfile = localStorage.getItem('userProfile');

  // Allow access if authenticated OR has local profile (onboarding complete)
  if (isAuthenticated || hasProfile) {
    return children;
  }

  return <Navigate to="/" replace />;
}

function AppContent() {
  const location = useLocation();
  const hideNav = ['/', '/onboarding', '/auth/callback', '/complete-profile'].includes(location.pathname);

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50">
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<MobileLogin />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/complete-profile" element={<CompleteProfile />} />

        {/* Protected routes - require login */}
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/matching" element={<ProtectedRoute><Matching /></ProtectedRoute>} />
        <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
        <Route path="/muhurtham" element={<ProtectedRoute><Muhurtham /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      </Routes>
      {!hideNav && <BottomNav />}
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
