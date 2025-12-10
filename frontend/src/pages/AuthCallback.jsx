/**
 * Auth Callback Page
 * Handles the redirect from Google OAuth
 */

import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';

export default function AuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { handleAuthCallback } = useAuth();
  const [status, setStatus] = useState('processing'); // processing, success, error
  const [message, setMessage] = useState('உள்நுழைகிறது...');

  useEffect(() => {
    const processCallback = async () => {
      const token = searchParams.get('token');
      const newUser = searchParams.get('new_user');
      const error = searchParams.get('error');

      if (error) {
        setStatus('error');
        setMessage('உள்நுழைவு தோல்வி. மீண்டும் முயற்சிக்கவும்.');
        setTimeout(() => navigate('/onboarding'), 2000);
        return;
      }

      if (token) {
        try {
          const result = await handleAuthCallback(token, newUser);
          if (result.success) {
            setStatus('success');
            setMessage('வெற்றிகரமாக உள்நுழைந்தீர்கள்!');

            // If new user (no astro profile), go to location collection
            if (result.isNewUser) {
              setTimeout(() => navigate('/complete-profile'), 1000);
            } else {
              setTimeout(() => navigate('/'), 1000);
            }
          } else {
            setStatus('error');
            setMessage('உள்நுழைவு தோல்வி.');
            setTimeout(() => navigate('/onboarding'), 2000);
          }
        } catch (err) {
          setStatus('error');
          setMessage('பிழை ஏற்பட்டது.');
          setTimeout(() => navigate('/onboarding'), 2000);
        }
      } else {
        setStatus('error');
        setMessage('தவறான அணுகல்.');
        setTimeout(() => navigate('/onboarding'), 2000);
      }
    };

    processCallback();
  }, [searchParams, handleAuthCallback, navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 flex items-center justify-center">
      <div className="text-center p-8">
        {/* Om Symbol */}
        <div className="mb-6">
          <span className="text-6xl text-orange-600 font-serif">ॐ</span>
        </div>

        {/* Status Icon */}
        <div className="mb-4">
          {status === 'processing' && (
            <Loader2 className="w-16 h-16 text-orange-500 animate-spin mx-auto" />
          )}
          {status === 'success' && (
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto" />
          )}
          {status === 'error' && (
            <XCircle className="w-16 h-16 text-red-500 mx-auto" />
          )}
        </div>

        {/* Message */}
        <p className="text-lg text-gray-700">{message}</p>

        {status === 'processing' && (
          <p className="text-sm text-gray-500 mt-2">சிறிது நேரம் காத்திருக்கவும்...</p>
        )}
      </div>
    </div>
  );
}
