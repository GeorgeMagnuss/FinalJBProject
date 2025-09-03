#!/bin/bash
echo "Testing complete login and stats flow..."

# Clean start
rm -f test_session.txt

# 1. Login
echo "1. Testing login..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8001/api/login/ \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"email":"admin@vacation.com","password":"admin123"}' \
  -c test_session.txt)
echo "Login response: $LOGIN_RESPONSE"

# 2. Test stats endpoints
echo -e "\n2. Testing vacation stats..."
STATS_RESPONSE=$(curl -s http://localhost:8001/api/stats/vacations/ \
  -H "Origin: http://localhost:3000" \
  -b test_session.txt)
echo "Vacation stats: $STATS_RESPONSE"

echo -e "\n3. Testing total users..."
USERS_RESPONSE=$(curl -s http://localhost:8001/api/total/users/ \
  -H "Origin: http://localhost:3000" \
  -b test_session.txt)
echo "Total users: $USERS_RESPONSE"

echo -e "\n4. Testing total likes..."
LIKES_RESPONSE=$(curl -s http://localhost:8001/api/total/likes/ \
  -H "Origin: http://localhost:3000" \
  -b test_session.txt)
echo "Total likes: $LIKES_RESPONSE"

echo -e "\n5. Testing likes distribution..."
DIST_RESPONSE=$(curl -s http://localhost:8001/api/distribution/likes/ \
  -H "Origin: http://localhost:3000" \
  -b test_session.txt)
echo "Likes distribution: ${DIST_RESPONSE:0:100}..."

# Cleanup
rm -f test_session.txt

echo -e "\nTest complete!"